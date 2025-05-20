using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class MainContractor : MainEntity , IHasCompany
{
    [Required] [MaxLength(255)]
    public string Name { get; set; }
    public string? ReferenceNo { get; set; }
    public bool HasUserAccount { get; set; } = true;
    public Guid CompanyId { get; set; }
    public Company Company { get; set; } = null!;
    public Guid? UserDetailId { get; set; }
    
    
    public UserDetail? UserDetail { get; set; }
    public ICollection<MainContractorProject> MainContractorProjects { get; set; } = new List<MainContractorProject>();
    
}