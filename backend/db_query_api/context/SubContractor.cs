using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class SubContractor : MainEntity , IHasCompany
{
    [Required] [MaxLength(255)]
    public string Name { get; set; }
    public string? ReferenceNo { get; set; }
    public bool HasUserAccount { get; set; } = true;

    public Guid CompanyId { get; set; }
    public Guid MainContractorId { get; set; }
    public Guid? UserDetailId { get; set; }
    public Guid SubContractorTypeId { get; set; }
    
    
    public SubContractorType SubContractorType { get; set; } = null!;
    
    public UserDetail? UserDetail { get; set; }
    public Company Company { get; set; } = null!;
    public MainContractor MainContractor { get; set; } = null!;
    
    public List<Employee> Employees { get; set; } = new List<Employee>();
}