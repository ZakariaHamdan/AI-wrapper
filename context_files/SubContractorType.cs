using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Permissions.Models;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;


public class SubContractorType : MainEntity, IHasCompany
{
    [Required] [MaxLength(255)]
    public string? NameEn { get; set; }
    [MaxLength(255)]
    public string NameAr { get; set; }
    public Guid CompanyId { get; set; }
    
    // Keep existing relationships but make virtual
    public virtual List<Employee>? Employees { get; set; } = new ();
    public Company Company { get; set; } = null!;


}