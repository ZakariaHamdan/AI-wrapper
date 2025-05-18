using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using BuildingBlock.Core.Files.Entities;
using BuildingBlock.Core.Files.Models;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Company : MainEntity, IHasFile
{
    [MaxLength(255)]
    public string? NameAr { get; set; }
    [Required] [MaxLength(255)]
    public string NameEn { get; set; }
    public string? ReferenceNo { get; set; }
    public bool HasUserAccount { get; set; } = true;
    
    // IHasFile implementation
    public Guid? FileId { get; set; }
    public FileData? File { get; set; }

    public List<MainContractor>? MainContractors { get; set; } = new List<MainContractor>(); 
}